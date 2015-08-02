#!/bin/bash

mkdir -p download;
cd download; 
rm *;
wget "http://twitchemotes.com/api_cache/v2/global.json";
wget "http://twitchemotes.com/api_cache/v2/subscriber.json";
