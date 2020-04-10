---


---

<h1 id="watchdog-readme">Watchdog README</h1>
<h1 id="requirements">Requirements</h1>
<pre><code>- docker-compose 3.7+
- WAMP / Nginx (optional for creating virtual hosts)
</code></pre>
<h1 id="setup">Setup</h1>
<h2 id="create-your-own-telegram-bot">Create your own Telegram Bot</h2>
<ol>
<li>Search for <strong>@BotFather</strong> on Telegram</li>
<li>In the chat with <strong>@BotFather</strong>, type <code>/start</code> to start the bot</li>
<li>Type <code>/newbot</code> to create a new bot and enter the desired username for your Bot</li>
</ol>
<blockquote>
<p><em>NOTE: Your bot name MUST end with the word “bot”, e.g. TetrisBot or Tetris_bot</em></p>
</blockquote>
<ol start="4">
<li>You have successfully created your bot, and will be given a bot token</li>
<li>Set a domain name to link your bot to, E.g. <a href="http://esdwatchdog.me">http://esdwatchdog.me</a></li>
</ol>
<blockquote>
<p><em>NOTE: You should provide a fully qualified domain name (FQDN). If not, refer to the following instructions to create your own Virtual Host with WAMP</em></p>
</blockquote>
<h2 id="create-your-own-virtual-host-with-wamp">Create Your Own Virtual Host with WAMP</h2>
<p>For this example, we will be using the <strong>WAMP</strong> stack for creating virtual hosts. However, you can use Nginx or  your preferred Apache stack.</p>
<ol>
<li>Turn on WAMP</li>
<li>Type <code>localhost</code> into your internet browser of your choice and enter.</li>
<li>Scroll down to <strong>Tools</strong> Section and select <strong>Add a Virtual Host</strong></li>
<li>Follow the instructions given on the page and complete the creation of your Virtual Host</li>
<li>Ensure the following ports are unused on your machine
<ul>
<li><strong>80 (Webapp)</strong></li>
<li><strong>1337 (Konga)</strong></li>
<li><strong>3306 (MySQL)</strong></li>
<li><strong>5002 (Healthcheck)</strong></li>
<li><strong>8000 (Konga)</strong></li>
<li>8080 (Phpmyadmin)</li>
<li>15672 (RabbitMQ Management UI)</li>
</ul>
</li>
</ol>
<blockquote>
<p><em>Services not bolded are optional and are not essential for the Watchdog app. However, if you choose to omit them remember to comment out these services in the <code>docker-compose.yml</code> file.</em></p>
</blockquote>
<h2 id="change-environment-variables">Change environment variables</h2>
<p>In <code>/env/.env.prod</code>, change the following variables:</p>
<p><code>WEBHOOK_ROUTE=/&lt;BOT-TOKEN&gt;</code></p>
<blockquote>
<p>Use the bot token of your own telegram bot.</p>
</blockquote>
<h2 id="webapp-configuration">Webapp Configuration</h2>
<p>In <code>/webapp/config.php</code>, change the following variables</p>
<pre><code># Telegram bot
$bot_username  -  Telegram Bot username
$bot_token     -  Telegram Bot token

# Domain configuration
$domain_name   -  Domain name
$hostname      -  Endpoint URI for kong service
</code></pre>
<h1 id="build">Build</h1>
<p>Open terminal of your choice, for this example we will be using <strong>Bash</strong>. Navigate to the project root and run</p>
<p><code>docker-compose up -d --build</code></p>
<p>The build process will take anywhere from 5 to 10 minutes depending on your internet connection and hardware. Once the build process has finished, run</p>
<p><code>docker ps</code></p>
<p>To check the state of your containers. If there some containers which are unhealthy, they could be raising errors since prerequisite services (RabbitMQ, SQL)may not be running yet.</p>
<p>However, if the container still refuses to boot, you can run</p>
<pre><code>docker-compose logs -f               --- View collective logs
docker logs -f &lt;container_id&gt;        --- Logs for single container
</code></pre>
<h1 id="kong-configuration">Kong Configuration</h1>
<p>After setting setting up the containers, we need to configure the Kong API gateway will require some additional configuration.</p>
<h2 id="creating-an-upstream-service">Creating an upstream service</h2>
<ol>
<li>Click on the <strong>Services</strong> tab on the sidebar</li>
<li>Add a new service with endpoint <a href="http://watchlist:5001">http://watchlist:5001</a></li>
<li>Configure the following routes for the service</li>
</ol>

<table>
<thead>
<tr>
<th align="center">Route</th>
<th align="center">Method</th>
<th align="center">Protocol</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">/watchlist/remove</td>
<td align="center">POST</td>
<td align="center">HTTP</td>
</tr>
<tr>
<td align="center">/watchlist/new</td>
<td align="center">POST, OPTIONS</td>
<td align="center">HTTP</td>
</tr>
<tr>
<td align="center">/contact/get</td>
<td align="center">GET</td>
<td align="center">HTTP</td>
</tr>
<tr>
<td align="center">/watchlist/get</td>
<td align="center">GET</td>
<td align="center">HTTP</td>
</tr>
</tbody>
</table>
