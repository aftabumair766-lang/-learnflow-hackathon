const express = require('express');
const app = express();
const PORT = process.env.PORT || 3001;

app.use(express.json());

// Health endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// TODO: Add endpoints from spec

app.listen(PORT, () => {
  console.log(`student-api listening on port ${PORT}`);
});
