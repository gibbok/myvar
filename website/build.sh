#!/bin/bash
go run cmd/generate-og-images/main.go
npx pagefind --site public --output-path public/pagefind
hugo
#x