import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types

from boffin.student.graphql import StudentMutation, StudentQuery, StudentSubscription
from boffin.student.rest import router as student_router

app = FastAPI(
    title="Boffin",
    description="[GraphQL](/graphql)",
)
app.include_router(student_router)


Query = merge_types(
    "Query",
    (StudentQuery,),
)
Mutation = merge_types(
    "Mutation",
    (StudentMutation,),
)
Subscription = merge_types(
    "Subscription",
    (StudentSubscription,),
)
schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
graphql_app: GraphQLRouter = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql", include_in_schema=False)
