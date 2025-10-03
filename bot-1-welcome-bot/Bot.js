require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMembers] });

client.once('ready', () => {
  console.log(`✅ Logged in as ${client.user.tag}`);
});

client.on('guildMemberAdd', (member) => {
  const channel = member.guild.systemChannel;
  if (channel) channel.send(`👋 Welcome to the server, ${member}!`);
  
  const role = member.guild.roles.cache.find(r => r.name === 'Member');
  if (role) member.roles.add(role);
});

client.on('guildMemberRemove', (member) => {
  const channel = member.guild.systemChannel;
  if (channel) channel.send(`😢 ${member.user.tag} has left the server.`);
});

client.login(process.env.DISCORD_TOKEN);
