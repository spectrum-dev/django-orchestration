from ariadne import (
    QueryType,
    make_executable_schema,
    load_schema_from_path,
    snake_case_fallback_resolvers,
    MutationType,
)

from authentication.graphql import IsAuthenticatedDirective

import authentication.resolvers
import strategy.resolvers
import authentication.resolvers
import orchestrator.resolvers

type_defs = [
    load_schema_from_path("authentication/schema.graphql"),
    load_schema_from_path("orchestration/schema.graphql"),
    load_schema_from_path("orchestrator/schema.graphql"),
    load_schema_from_path("strategy/schema.graphql"),
]

# Query Implementations
query = QueryType()
query.set_field(
    "accountWhitelistStatus", authentication.resolvers.get_account_whitelist_status
)
query.set_field("ping", authentication.resolvers.get_ping)
query.set_field("allMetadata", orchestrator.resolvers.get_all_metadata)
query.set_field("userStrategies", strategy.resolvers.list_user_strategies)
query.set_field("strategies", strategy.resolvers.list_strategies)
query.set_field("sharedUsers", strategy.resolvers.list_shared_users)
query.set_field("taskResult", strategy.resolvers.get_task_result)
query.set_field(
    "inputDependencyGraph", orchestrator.resolvers.get_input_dependency_graph
)

# Mutation Implementations
mutation = MutationType()

mutation.set_field("dispatchRunStrategy", strategy.resolvers.dispatch_run_strategy)
mutation.set_field("shareStrategy", strategy.resolvers.share_strategy)

# Directives
directives = {
    "isAuthenticated": IsAuthenticatedDirective,
}

schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers, directives=directives
)
