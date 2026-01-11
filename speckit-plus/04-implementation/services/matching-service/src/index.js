const express = require('express');
const app = express();
const PORT = process.env.PORT || 3003;

app.use(express.json());

// Health endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// TODO: Add endpoints from spec

app.listen(PORT, () => {
  console.log(`matching-service listening on port ${PORT}`);
});
