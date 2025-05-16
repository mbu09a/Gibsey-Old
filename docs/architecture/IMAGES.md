# Docker Image Versioning Policy

## Overview

This document outlines the versioning and tagging strategy for Gibsey's Docker images. The goal is to ensure immutability, traceability, and reproducibility of all containerized components.

## Tagging Convention

All Docker images are tagged with the Git commit SHA that was used to build them. This provides an immutable reference to the exact code that was used to create the image.

### Format

```
ghcr.io/gibsey/<service>:<git-sha>
```

### Examples

- `ghcr.io/gibsey/gibsey-backend:a1b2c3d4e5f6...`
- `ghcr.io/gibsey/gibsey-frontend:a1b2c3d4e5f6...`

## Building Images

To build and tag images, use the provided script:

```bash
./scripts/build_and_tag.sh
```

This script will:
1. Get the current Git SHA
2. Build and tag both backend and frontend images with the SHA
3. Print the fully qualified image names

## Pushing Images

After building, you can push the images to the container registry:

```bash
docker push ghcr.io/gibsey/gibsey-backend:$(git rev-parse HEAD)
docker push ghcr.io/gibsey/gibsey-frontend:$(git rev-parse HEAD)
```

## Best Practices

1. **Always use SHA tags in production** - Never use `latest` or other mutable tags in production environments.
2. **Never re-tag images** - Each image should be built once and never modified.
3. **Reference images by full SHA** - For maximum reproducibility, use the full image digest in production manifests.
4. **Keep build environments consistent** - Use the pinned base images specified in the Dockerfiles.

## CI/CD Integration

In your CI/CD pipeline, you can use the following pattern:

```yaml
steps:
  - name: Build and push images
    run: |
      ./scripts/build_and_tag.sh
      echo "GIT_SHA=$(git rev-parse HEAD)" >> $GITHUB_ENV
    
  - name: Push to registry
    run: |
      echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
      docker push ghcr.io/gibsey/gibsey-backend:${{ env.GIT_SHA }}
      docker push ghcr.io/gibsey/gibsey-frontend:${{ env.GIT_SHA }}
```

## Rollbacks

To rollback to a previous version:
1. Checkout the desired commit: `git checkout <commit-sha>`
2. Run the build script: `./scripts/build_and_tag.sh`
3. Deploy the resulting images
