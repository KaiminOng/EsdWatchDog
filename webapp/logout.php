<?php

if (isset($_COOKIE['tg_user'])) {
    setcookie('tg_user', '',time() - 3600, '/', 'esdwatchdog.com');
    header('Location: /');
    die();
} else {
    $_SESSION['errors'] = 'unauthorized';
    header("Location: /");
    die();
}
