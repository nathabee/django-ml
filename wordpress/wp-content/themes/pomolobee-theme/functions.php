<?php
add_action('wp_enqueue_scripts', function() {
  wp_enqueue_style('pomolobee-style', get_stylesheet_uri(), [], wp_get_theme()->get('Version'));
});

 
add_action('after_setup_theme', function () {
  add_theme_support('custom-logo', ['flex-width'=>true,'flex-height'=>true]);
});