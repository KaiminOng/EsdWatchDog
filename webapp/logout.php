<?php
include "config.php";

if (isset($_COOKIE['tg_user'])) {
    setcookie('tg_user', '',time() - 3600, '/', 'esdwatchdog.me');
    header('Location: /');
    die();
} else {
    header("Location: /");
    die();
}
?>