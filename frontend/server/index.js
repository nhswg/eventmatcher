import { createServer } from "http";
import { Server } from "socket.io";

const httpServer = createServer();
const io = new Server(httpServer, {
    cors: {
      origin: "http://localhost:5173",
      //origin:"*", //for all
      methods: ["GET"],
      credentials: true
  }
});
