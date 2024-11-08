#!/bin/bash

SECRET_DIR=./secrets

mkdir -p "$SECRET_DIR"

db_root_password=$(openssl rand -base64 24)
echo "$db_root_password" > "$SECRET_DIR/db_root_password"

db_password=$(openssl rand -base64 24)
echo "$db_password" > "$SECRET_DIR/db_password"

secret_key=$(openssl rand -base64 32)
echo "$secret_key" > "$SECRET_DIR/secret_key"
