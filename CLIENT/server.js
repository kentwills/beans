const express = require('express');
const path = require('path');

const app = express();

app.use("/js", express.static(__dirname + "/dist/bundle/"));
app.use("/css", express.static(__dirname + "/static/css/"));
app.use("/img", express.static(__dirname + "/static/img/"));

app.get('/', (req, res) => {
  res.sendFile(path.resolve(__dirname, 'user_pages.html'));
});

// Start the server
const PORT = process.env.PORT || 9000;
app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
});
