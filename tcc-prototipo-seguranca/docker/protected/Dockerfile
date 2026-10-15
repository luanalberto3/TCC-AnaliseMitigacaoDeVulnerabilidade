FROM php:8.3-apache

RUN docker-php-ext-install pdo_mysql \
    && a2enmod headers

COPY docker/protected/app/ /var/www/html/
COPY mitigacao/ /var/www/html/includes/

RUN chown -R www-data:www-data /var/www/html
