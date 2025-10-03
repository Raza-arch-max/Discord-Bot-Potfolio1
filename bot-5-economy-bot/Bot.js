require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');
const mongoose = require('mongoose');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });
const PREFIX = '!';

mongoose.connect(process.env.MONGO_URI);

const userSchema = new mongoose.Schema({
  userId: String,
  balance: Number,
});

const User = mongoose.model('User', userSchema);

client.once('ready', () => {
  console.log(`💰 Economy Bot online as ${client.user.tag}`);
});

client.on('messageCreate', async (message) => {
  if (message.author.bot || !message.content.startsWith(PREFIX)) return;

  const [command] = message.content.slice(PREFIX.length).split(' ');

  if (command === 'balance') {
    let user = await User.findOne({ userId: message.author.id });
    if (!user) {
      user = await User.create({ userId: message.author.id, balance: 100 });
    }
    message.reply(`💵 You have $${user.balance}`);
  }

  if (command === 'daily') {
    let user = await User.findOne({ userId: message.author.id });
    if (!user) user = await User.create({ userId: message.author.id, balance: 100 });
    user.balance += 50;
    await user.save();
    message.reply(`✅ You claimed daily $50. Total: $${user.balance}`);
  }
});

client.login(process.env.DISCORD_TOKEN);
