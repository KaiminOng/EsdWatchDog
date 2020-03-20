<?php
// header('Access-Control-Allow-Origin: http://esdwatchdog.com/');
// header('Access-Control-Allow-Credentials: true');
// session_start();

define('BOT_USERNAME', '@ESD_Proj_bot'); // place username of your bot here

var_dump($_COOKIE);

if (isset($_COOKIE['tg_user'])){
  $user_info = json_decode($_COOKIE['tg_user'], true);
  // print_r($_COOKIE['tg_user']);
  $user_id = $user_info['id'];
  echo "USER ID:".$user_info['id'];
}

function getTelegramUserData() {
  if (isset($_COOKIE['tg_user'])) {
    $auth_data_json = urldecode($_COOKIE['tg_user']);
    $auth_data = json_decode($auth_data_json, true);
    return $auth_data;
  }
  return false;
}

// if(isset($_SESSION['tg_user'])){
//   $user_info = json_decode($_SESSION['tg_user'], true);
//   // $user_id = $user_info['id'];
//   // echo "USER ID:".$user_info['id'];
//   var_dump($_SESSION['tg_user']);
// }

// function getTelegramUserData() {
//   if (isset($_SESSION['tg_user'])) {
//     $auth_data_json = urldecode($_SESSION['tg_user']);
//     $auth_data = json_decode($auth_data_json, true);
//     return $auth_data;
//   }
//   return false;
// }

if (isset($_GET['logout'])) {
  setcookie('tg_user', '');
  // session_destroy();
  header('Location: /');
}

$tg_user = getTelegramUserData();
if ($tg_user !== false) {
  // var_dump($tg_user);
  $first_name = htmlspecialchars($tg_user['first_name']);

  if (isset($tg_user['last_name'])){
    $last_name = htmlspecialchars($tg_user['last_name']);
  } else{
    $last_name = '';
  }
  
  if (isset($tg_user['username'])) {
    $username = htmlspecialchars($tg_user['username']);
    $html = "<h1>Hello, <a href=\"https://t.me/{$username}\">{$first_name} {$last_name}</a>!</h1>";
  } else {
    $html = "<h1>Hello, {$first_name} {$last_name}!</h1>";
  }

  if (isset($tg_user['photo_url'])) {
    $photo_url = htmlspecialchars($tg_user['photo_url']);
    $html .= "<img src=\"{$photo_url}\">";
  }

  $html .= "<p><a href=\"?logout=1\">Log out</a></p>";
} else {
  $bot_username = BOT_USERNAME;

  $html = <<<HTML
<h1>Hello, anonymous!</h1>
<script async src="https://telegram.org/js/telegram-widget.js?7" data-telegram-login="ESD_Proj_bot" data-size="large"  data-auth-url="microservices/authentication/authentication.php" data-request-access="write"></script>
      
HTML;

}

  echo <<<HTML
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>G5T6 WatchDog</title>
  </head>
  <body><center>{$html}</center>
    
  </body>
</html>
HTML;

?>