<?php
// header('Access-Control-Allow-Origin: http://esdwatchdog.com/');
// header('Access-Control-Allow-Credentials: true');
// session_start();

define('BOT_USERNAME', 'ESD_Proj_bot'); // place username of your bot here

$bot_username = BOT_USERNAME;


?>
<html>
  <head>
    <meta charset="utf-8">
    <title>G5T6 WatchDog</title>

    <link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:200,300,400,600,700,900" rel="stylesheet" />
    <link href="src/default.css" rel="stylesheet" type="text/css" media="all" />
    <link href="src/fonts.css" rel="stylesheet" type="text/css" media="all" />

    <!--[if IE 6]><link href="default_ie6.css" rel="stylesheet" type="text/css" /><![endif]-->

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>

    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>

  </head>
  <body>
  <div id="page" class="container">
    <div id="header" style="width:1200px;">
      <div id="logo">
        <br><br>
        <center><h1 style="color:#6c7ae0">G4T7 Watchdog Application</h1>
        <span style="font-size:20px">Where You Can Monitor With Ease</span>
        </center>
      </div>
      <div id="menu">
      <center>
          <script async src="https://telegram.org/js/telegram-widget.js?7" data-telegram-login=<?= $bot_username?> data-size="large"  data-auth-url="authentication/authentication.php" data-request-access="write"></script>
        </center>
      </div>
    </div>
    
  </div>
  </body>
</html>