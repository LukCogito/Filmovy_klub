<?php
    error_log("Zpráva o chybě", 3, "error.log");
    $link = $_POST['link'];
    $file = fopen('data/odkazy.csv', 'a');
    fputcsv($file, array($link));
    fclose($file);
    header('Location: http://sulis125.zcu.cz/');
?>
