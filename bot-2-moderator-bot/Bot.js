require('dotenv').config();
const { Client, GatewayIntentBits, PermissionsBitField } = require('discord.js');

const PREFIX = '!';

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent, GatewayIntentBits.GuildMembers] });

client.once('ready', () => {
  console.log(`✅ Moderator Bot online as ${client.user.tag}`);
});

client.on('messageCreate', async (message) => {
  if (!message.content.startsWith(PREFIX) || message.author.bot) return;

  const [command, ...args] = message.content.trim().substring(PREFIX.length).split(/\s+/);

  if (command === 'kick') {
    if (!message.member.permissions.has(PermissionsBitField.Flags.KickMembers)) return message.reply("No permission!");
    const member = message.mentions.members.first();
    if (member) {
      await member.kick();
      message.channel.send(`👢 Kicked ${member.user.tag}`);
    }
  }

  if (command === 'ban') {
    if (!message.member.permissions.has(PermissionsBitField.Flags.BanMembers)) return message.reply("No permission!");
    const member = message.mentions.members.first();
    if (member) {
      await member.ban();
      message.channel.send(`⛔ Banned ${member.user.tag}`);
    }
  }

  if (command === 'clear') {
    const count = parseInt(args[0], 10);
    if (isNaN(count) || count < 1 || count > 100) return message.reply("Use: `!clear <1-100>`");
    await message.channel.bulkDelete(count, true);
    message.channel.send(`🧹 Cleared ${count} messages`).then(msg => setTimeout(() => msg.delete(), 3000));
  }
});

client.login(process.env.DISCORD_TOKEN);
