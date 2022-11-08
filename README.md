# SSL Terminating NGINX reverse proxy with Vaultwarden and CouchDB as backend 
---
### To run the composition you need to:
- Add your own NGINX configuration files to `./data/nginx/` (namely, the nginx.conf file as well as site configs, for the latter see the Vaultwarden repository with examples)
- create .env file for the env variables DOMAIN, NGINX_PORT and COUCH_PORT

Now, simply run docker compose for the services you want to start!

### Backup Script
To use the backup script you have to install create a public/private key-pair and put the public key to `./backupper/secrets/`. Move your private key to a safe place where you will not lose it and, espcially, nobody but you can access it. I created two (redundancy!) USB sticks containing the private key and deposited at two different physical locations.

Next you have to install rsync and adapt [Line 45](https://github.com/pxbn/nginx-fronted-bw/blob/b3d0e7e188f0dee7493e248a56b66c5ac7586fc1/backupper/backupper.py#L45)  for your rsync configuration.

Have fun!
