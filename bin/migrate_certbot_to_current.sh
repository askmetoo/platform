#!/bin/bash -e

OLD_CERTBOT=/var/snap/platform/common/certbot
NEW_CERTBOT=/var/snap/platform/current/certbot

RENEWAL_DIR=$NEW_CERTBOT/renewal
if [[ -d $RENEWAL_DIR ]]; then
    sed -i 's#'$OLD_CERTBOT'#'$NEW_CERTBOT'#g' $RENEWAL_DIR/*.conf
fi