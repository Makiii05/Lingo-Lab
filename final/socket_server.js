const { Server } = require("socket.io");

const io = new Server(3001, {
    cors: { origin: "*" }
});

io.on("connection", (socket) => {
    console.log("Connected:", socket.id);

    socket.on("quiz_elapsed", (data) => {
        console.log("ELAPSED:", data);
        io.emit("mentor_elapsed", data);  // send to Django
    });
});
