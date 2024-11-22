const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

// User schema for authentication
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  passwordHash: { type: String, required: true },
});

// Article schema for fetching articles
const articleSchema = new mongoose.Schema({
  Date: Date,
  Title: String,
  Content: String,
  Sentiment_Score: Number,
});

// Define models
const User = mongoose.model('User', userSchema);
const Article = mongoose.model('Article', articleSchema, 'Apple');

const app = express();
app.use(cors());
app.use(express.json());

// MongoDB connection
const password = encodeURIComponent("qwertyuiop");
const uri = `mongodb+srv://EchoTrade:${password}@echo-trade.ujnvr.mongodb.net/NewsData?retryWrites=true&w=majority&appName=Echo-Trade`;
mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB'))
  .catch((error) => console.error('MongoDB connection error:', error));

// Authentication middleware
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Access denied' });
  try {
    const verified = jwt.verify(token, 'your_secret_key');
    req.user = verified;
    next();
  } catch (error) {
    res.status(400).json({ error: 'Invalid token' });
  }
};

// User signup
app.post('/api/signup', async (req, res) => {
  const { email, password } = req.body;
  try {
    const salt = await bcrypt.genSalt(10);
    const passwordHash = await bcrypt.hash(password, salt);
    const newUser = new User({ email, passwordHash });
    await newUser.save();
    res.status(201).json({ message: 'User created successfully' });
  } catch (error) {
    res.status(400).json({ error: 'Error creating user' });
  }
});

// User login
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  try {
    const user = await User.findOne({ email });
    if (!user) return res.status(404).json({ error: 'User not found' });

    const isPasswordValid = await bcrypt.compare(password, user.passwordHash);
    if (!isPasswordValid) return res.status(401).json({ error: 'Invalid password' });

    const token = jwt.sign({ id: user._id, email: user.email }, 'your_secret_key', { expiresIn: '1h' });
    res.json({ token, user: { id: user._id, email: user.email } });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Profile route
app.get('/api/profile', authenticate, (req, res) => {
  res.json({ user: { email: req.user.email } });
});

// Articles route (with authentication)
app.get('/api/aapl/articles', authenticate, async (req, res) => {
  try {
    const articles = await Article.find(); // Fetch articles from the 'Apple' collection
    res.json(articles);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching articles' });
  }
});

// Start the server
const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
