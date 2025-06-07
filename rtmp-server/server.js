/**
 * Simple RTMP server using node-media-server
 *
 * Usage: node server.js
 *
 * RTMP URL: rtmp://<your_ip>:1935/live/stream
 */

const NodeMediaServer = require('node-media-server');
const os = require('os');

const config = {
  rtmp: {
    port: 1935,
    host: '0.0.0.0', // permite acesso externo
    chunk_size: 60000,
    gop_cache: true,
    ping: 30,
    ping_timeout: 60
  },
  http: {
    port: 8000,
    host: '0.0.0.0', // permite acesso externo
    allow_origin: '*'
  }
};

function getLocalIP() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal && !iface.address.startsWith('172.')) {
        return iface.address;
      }
    }
  }
  return 'localhost';
}

const nms = new NodeMediaServer(config);
nms.run();

const localIP = getLocalIP();
console.log('\n✅ RTMP server running!');
console.log(`➡️  Send your stream to: rtmp://${localIP}:1935/live/stream`);
console.log(`🌐 Web panel: http://${localIP}:8000`);
console.log('📱 Set this as the RTMP endpoint on your Android camera app.');
