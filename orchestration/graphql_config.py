from ariadne import (
    QueryType,
    make_executable_schema,
    load_schema_from_path,
    snake_case_fallback_resolvers,
    MutationType,
)

from authentication.graphql import IsAuthenticatedDirective

import strategy.resolvers
import authentication.resolvers

type_defs = [
    load_schema_from_path("orchestration/schema.graphql"),
    load_schema_from_path("strategy/schema.graphql"),
]

# Query Implementations
query = QueryType()
query.set_field("ping", authentication.resolvers.get_ping)
query.set_field("userStrategies", strategy.resolvers.list_user_strategies)
query.set_field("strategies", strategy.resolvers.list_strategies)
query.set_field("taskResult", strategy.resolvers.get_task_result)

# Mutation Implementations
mutation = MutationType()
mutation.set_field("dispatchRunStrategy", strategy.resolvers.dispatch_run_strategy)

# Directives
directives = {
    "isAuthenticated": IsAuthenticatedDirective,
}

schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers, directives=directives
)
