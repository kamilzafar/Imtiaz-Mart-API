#!/bin/sh

KONG_ADMIN_URL="http://localhost:8001"

# Wait for Kong to be ready
until $(curl --output /dev/null --silent --head --fail $KONG_ADMIN_URL); do
  printf '.'
  sleep 5
done

# Register todo
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=service1" \
  --data "url=http://host.docker.internal:8003"

# Register todo-service route
curl -i -X POST $KONG_ADMIN_URL/services/service1/routes \
  --data "paths[]=/service1" \
  --data "strip_path=true"

# Register service2
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=service2" \
  --data "url=http://host.docker.internal:8004"

# Register service2 route
curl -i -X POST $KONG_ADMIN_URL/services/service2/routes \
  --data "paths[]=/service2" \
  --data "strip_path=true"

# Register service3
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=service3" \
  --data "url=http://host.docker.internal:8005"

# Register service3 route
curl -i -X POST $KONG_ADMIN_URL/services/service3/routes \
  --data "paths[]=/service3" \
  --data "strip_path=true"

# Register service4
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=service4" \
  --data "url=http://host.docker.internal:8006"

# Register service4 route
curl -i -X POST $KONG_ADMIN_URL/services/service4/routes \
  --data "paths[]=/service4" \
  --data "strip_path=true"

# Register service5
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=service5" \
  --data "url=http://host.docker.internal:8007"

# Register service5 route
curl -i -X POST $KONG_ADMIN_URL/services/service5/routes \
  --data "paths[]=/service5" \
  --data "strip_path=true"

# Register service6
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=service6" \
  --data "url=http://host.docker.internal:8008"

# Register service6 route
curl -i -X POST $KONG_ADMIN_URL/services/service6/routes \
  --data "paths[]=/service6" \
  --data "strip_path=true"

# Register merged spec service
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=specs-combiner" \
  --data "url=http://host.docker.internal:9000"

# Register merged spec route
curl -i -X POST $KONG_ADMIN_URL/services/specs-combiner/routes \
  --data "paths[]=/specs-combiner" \
  --data "strip_path=true"

# Register kong-spec-expose plugin
# curl -i -X POST $KONG_ADMIN_URL/services/spec-server/plugins \
#   --data "name=kong-spec-expose" \
#   --data "config.spec_url=http://localhost:8000/merge/openapi.json"