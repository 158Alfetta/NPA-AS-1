import express from 'express';
import { ApolloServer } from 'apollo-server-express'
import schema from './graphql'
import './mongoose-connect'

const server = new ApolloServer({
    schema,
    playground: true,
});

const app = express();
server.applyMiddleware({ app });

app.listen({ port: 5001 }, () =>
  console.log(`🚀 Server ready at http://localhost:5001${server.graphqlPath}`)
);