#!/bin/bash
go run cmd/generate-og-images/main.go
hugo
npx pagefind --site public