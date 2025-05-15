Below is a conceptual design for a lightweight “Chaos-Mirror Orchestrator” capable of automatically spinning up, snapshotting, and pruning VPS nodes in a manner that reports live health, all while ensuring near-continuous availability (5‑nines) within a **strict budget of <\$30/mo**. The design is “swarm-aware” in that it leverages a minimal cluster overlay (e.g., Docker Swarm or K3s) and uses a distributed key/value or secret store (Vault) for health and state coordination.

---

## 1. High-Level Architecture

### 1.1 Components Overview

1. **Chaos-Mirror Orchestrator (CMO)**

   * A small automation layer (could be built with Terraform + Ansible, or custom scripts) that:

     * Interacts with multiple cheap VPS providers’ APIs (Vultr, DigitalOcean, Linode, etc.).
     * Provisions new VPS nodes on-demand.
     * Snapshots nodes and prunes them once they are no longer needed.
     * Reports node lifecycle events (create/boot, snapshot complete, prune complete) back into **Vault**.

2. **Vault for Health and Secrets**

   * A distributed Vault cluster (or Vault “shards”) that:

     * Stores cluster secrets (encryption keys, orchestration secrets).
     * Maintains a global health state for each node (“live,” “degraded,” “snapshotting,” “retiring,” etc.).
   * Each node runs a Vault agent or sidecar. The Orchestrator uses Vault’s APIs to mark node states.

3. **Swarm/K3s**

   * A minimal cluster overlay that:

     * Schedules container workloads across the nodes.
     * Provides a stable network overlay for service discovery.
     * The orchestrator checks the swarm health to determine whether a node is truly “healthy” (in addition to raw VPS health checks).

4. **(Optional) Load Balancer Layer**

   * A cheap or “free-tier” load balancer (e.g., using something like HAProxy on a \$5 node, or AWS free-tier ALB if desired).
   * Routes inbound requests to healthy nodes in the cluster.

5. **Monitoring & Alerting**

   * A small Prometheus + Alertmanager stack (can be co-located on a single node if resource usage is minimal) or a third-party free-tier monitoring (e.g., UptimeRobot).
   * Sends messages if nodes go down, or if any orchestrator action fails repeatedly.

### 1.2 Sample Providers & Cost Outline

* **Provider Mix**

  * **DigitalOcean (\$5 Droplets):** 2–3 droplets spread across regions.
  * **Vultr/Hetzner (\$3.50–\$5 Instances):** 1–2 droplets in different regions.
  * **Oracle Cloud Free Tier** for small workloads or load balancer.
* **Estimated Costs**

  * Target 4–5 small VPS nodes total: \$5–\$20 (depending on exact plan).
  * 1 node dedicated to the load balancer and minimal monitoring: \$5.
  * **Total:** \~\$25 max to leave margin for snapshot storage or egress, staying under \$30.

Note that ephemeral snapshots often incur minimal storage cost, especially if quickly pruned or if using block storage on discount tiers. The orchestrator’s job is to ensure snapshots never linger beyond their retention window.

---

## 2. Infrastructure Diagram

```
                       +----------------------+
                       |  Chaos-Mirror       |
                       |  Orchestrator (CMO) |
                       |  (Terraform, etc.)  |
                       +---------+-----------+
                                 |
              +------------------v-------------------+
              |        Vault + Monitoring           |
              | (distributed across cluster nodes)   |
              +----------------+----------------------+
                               | gossip / API
          +--------------------+----------------------+
          |     Swarm/K3s overlay network            |
          +---+----------------+----------------+-----+
              |                |                |
   +----------v--------+  +----v----------+  +--v-----------+
   | VPS Node (A)      |  | VPS Node (B)  |  | VPS Node (C) |
   | - Vault agent     |  | - Vault agent |  | - Vault agent|
   | - Docker/K3s, etc.|  | - Docker/K3s  |  | - Docker/K3s |
   +-------------------+  +---------------+  +--------------+
```

1. **Chaos-Mirror Orchestrator** orchestrates node creation, destruction, snapshot, etc.
2. **Vault + Monitoring** can run in a distributed manner on each VPS node (or a single dedicated node, depending on scale).
3. **Swarm/K3s** ensures container workloads are balanced across nodes.

---

## 3. Fail-Over Algorithm

Below is a simplified step-by-step of how the system responds to node failures (or graceful retirements):

1. **Periodic Health Check**

   * Each node self-reports to Vault (e.g., “I am alive” with a timestamp).
   * The Orchestrator polls the cluster overlay (Swarm/K3s) to confirm scheduling status is healthy.
   * If node checks fail or degrade, the node is marked as “unhealthy” in Vault.

2. **Snapshot & Prune**

   * If the node is still partially reachable (preemptive retirement scenario), Orchestrator triggers a final snapshot (image) to the VPS provider.
   * If the node is fully gone, skip snapshot and proceed to prune it from the cluster.

3. **Spin Up Replacement**

   * Orchestrator requests a new VPS from the same or alternate provider.
   * Optionally uses the snapshot of the retired node to restore data or joins an existing cluster bootstrapping process.
   * Writes new node metadata (IP, region, provider, etc.) to Vault.

4. **Rejoin Cluster**

   * New node auto-installs Swarm/K3s, Vault agent, and relevant containers via user-data or provisioning scripts.
   * Swarm rebalances workloads from unhealthy node to the new node.

5. **Confirm Full Health**

   * Vault sees new node heartbeat.
   * Orchestrator sets new node to “active.”
   * Freed snapshot images are pruned if older than the retention window to save costs.

6. **Scale Check**

   * If repeated node failures occur in one region, the Orchestrator may shift capacity to other regions (still within the cost budget).

**Availability Note**: The combination of a minimal load-balancing approach (point traffic to the healthy nodes) plus automatic provisioning ensures near 5-nines availability, albeit with the constraint that node startup can take \~1–2 min. This design aims to keep downtime minimal in practice.

---

## 4. Disaster Drill Test Matrix

This matrix outlines scenarios to test the resiliency of the Chaos-Mirror Orchestrator. Each scenario verifies failover, orchestration, and cost controls remain intact.

| **Test ID** | **Scenario**                     | **Procedure**                                                                                                          | **Expected Outcome**                                                                                                          |
| ----------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 1           | **Single Node Crash**            | 1. Force-shutdown 1 node (kill -9 or stop VM). <br>2. Wait for orchestrator to detect.                                 | - Node is marked “unhealthy.” <br>- Orchestrator spins up replacement node. <br>- Vault status returns healthy with new node. |
| 2           | **Node Loses Network**           | 1. Block network traffic for 1 node (firewall rule). <br>2. Monitor node health in Vault.                              | - Node transitions to “degraded” then “unhealthy.” <br>- Automatic re-provisioning triggered in alternative region.           |
| 3           | **Final Snapshot Failure**       | 1. Induce error on snapshot creation (e.g., invalid credentials, out-of-quota). <br>2. Orchestrator attempts snapshot. | - Snapshot fails, orchestrator logs error. <br>- Node forcibly pruned (no snapshot). <br>- Replacement node launched.         |
| 4           | **Vault Outage**                 | 1. Temporarily stop Vault on 1 node. <br>2. Observe cluster operation.                                                 | - Vault cluster re-routes to remaining healthy Vault shards. <br>- No orchestrator disruption.                                |
| 5           | **Orchestrator State Loss**      | 1. Simulate orchestrator ephemeral storage wipe. <br>2. Relaunch orchestrator container.                               | - Orchestrator re-initializes from Vault. <br>- Continues normal operation with historical cluster state from Vault.          |
| 6           | **Multiple Nodes Crash**         | 1. Simultaneously kill 2 nodes in the same region. <br>2. Observe cluster capacity and load balancer behavior.         | - Remaining node(s) handle traffic at degraded capacity. <br>- Orchestrator spins up 2 replacements, rebalances cluster.      |
| 7           | **Cost Overrun / Quota Reached** | 1. Force repeated node spin-ups to exceed monthly node budget. <br>2. Observe how orchestrator responds.               | - Orchestrator halts new node creation and logs “budget exhausted.” <br>- Alert triggered for manual intervention.            |
| 8           | **Slow Node Boot**               | 1. Force a slow or hung boot on new node. <br>2. Swarm indicates new node is not ready.                                | - Orchestrator times out, marks node as failed. <br>- Orchestrator tries next provider or region.                             |
| 9           | **Snapshot Prune Validation**    | 1. Create many snapshots quickly. <br>2. Let retention policy expire. <br>3. Validate automatic pruning.               | - Snapshots older than retention window are pruned from provider. <br>- Orchestrator logs successful prune events.            |
| 10          | **Full Region Outage**           | 1. Stop entire region (simulate provider region failure). <br>2. Validate cluster continuity in other regions.         | - Orchestrator spins up nodes in alternate region(s). <br>- Load balancer routes all traffic to healthy region(s).            |

---

## 5. Key Points to Achieve <\$30/Month

1. **Use Small Instances**: e.g., \$5 or \$3.50 tiers.
2. **Limit Node Count**: Aim for 4–5 nodes total.
3. **Prune Snapshots Aggressively**: Only keep 1–2 snapshots per node.
4. **Spot / Free-tier LB**: Consider single-node HAProxy or a free-tier LB for incoming traffic.
5. **Leverage Provider Discounts**: Some providers offer free internal data transfer or promotional credits for new accounts.

---

## 6. Summary

By combining a minimal cluster overlay (Docker Swarm or K3s), a distributed Vault instance for state and health checks, and an orchestrator (Chaos-Mirror Orchestrator) that can talk to multiple low-cost VPS providers, this design meets the following goals:

1. **Automatic Node Lifecycle**: Spin up, snapshot, prune.
2. **Health Reporting**: Real-time node statuses stored in Vault.
3. **High Availability**: Fail-over in under 1–2 minutes, targeting 99.999% availability.
4. **Cost Control**: Pruned snapshots, minimal node footprints, and free-tier/low-tier LB/monitoring keep total monthly spending under \$30.

The attached **fail-over algorithm** and **test matrix** ensure we systematically validate every major failure scenario, helping confirm that the “Chaos-Mirror Orchestrator” lives up to its name—resilient, chaos-tested, and cost-aware.