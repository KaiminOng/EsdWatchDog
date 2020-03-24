<?php
session_start();

if(!isset($_SESSION['tg_user'])){
    header('Location: /');
}
?>