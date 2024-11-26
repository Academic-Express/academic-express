#!/bin/bash

SECRET_DIR=./secrets

mkdir -p "$SECRET_DIR"

write_secret() {
    local secret_name=$1
    local secret_value=$2

    local secret_file="$SECRET_DIR/$secret_name"
    if [ -f "$secret_file" ]; then
        read -p "File $secret_file already exists. Overwrite? [y/N] " choice
        if [ "${choice,,}" != "y" ]; then
            echo "Skipping $secret_name"
            return
        fi
    fi

    echo "$secret_value" > "$secret_file"
    echo "Generated $secret_name"
}

write_secret db_root_password "$(openssl rand -base64 24)"
write_secret db_password "$(openssl rand -base64 24)"
write_secret secret_key "$(openssl rand -base64 32)"
write_secret feed_engine_token "$(openssl rand -base64 24)"
