<?php
// session_start();

define('BOT_USERNAME', '@ESD_Proj_bot'); // place username of your bot here


if (isset($_COOKIE['tg_user'])){
  $user_info = json_decode($_COOKIE['tg_user'], true);
  print_r($_COOKIE['tg_user']);
  // $user_id = $user_info['id'];
  // echo "USER ID:".$user_info['id'];

}

function getTelegramUserData() {
  if (isset($_COOKIE['tg_user'])) {
    $auth_data_json = urldecode($_COOKIE['tg_user']);
    $auth_data = json_decode($auth_data_json, true);
    return $auth_data;
  }
  return false;
}

if (isset($_GET['logout'])) {
  setcookie('tg_user', '');
  // session_destroy();
  header('Location: /');
}

$tg_user = getTelegramUserData();
if ($tg_user !== false) {
  
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
  $html .= "<a id='sendBtn' class='btn btn-primary'>Send A Message</a>";
  $html .= "<p><a href=\"?logout=1\">Log out</a></p>";
} else {
  $bot_username = BOT_USERNAME;

  $html = <<<HTML
<h1>Hello, anonymous!</h1>
<script async src="https://telegram.org/js/telegram-widget.js?7" data-telegram-login="ESD_Proj_bot" data-size="large"  data-auth-url="check_authorization.php" data-request-access="write"></script>
      
HTML;


}

  echo <<<HTML
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Login Widget Example</title>
  </head>
  <body><center>{$html}</center>
    <script>
      $('#sendBtn').click(async (event) => {
          //Prevents screen from refreshing when submitting
          event.preventDefault();

          // Change serviceURL to your own
          var serviceURL = "http://localhost:300/send_message/" + {$user_id};
          
          try {
              const response =
              await fetch(
                  serviceURL, {
                  method: 'POST',
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ title: title, price: price, 
                      availability: availability})
              });

              const data = await response.json();
              console.log(data);
              if (data[1] === 400){
                  document.getElementById("message").innerHTML = data[0].message
              }
              else if(data[1] === 201){
                  document.getElementById("message").innerHTML = title + " has been succesfully added."
              }

          } catch (error) {
              // Errors when calling the service; such as network error, 
              // service offline, etc
              showError
          ('There is a problem adding the book, please try again later.<br />'+error);
          
          } // error
      });
    </script>
  </body>
</html>
HTML;

?>