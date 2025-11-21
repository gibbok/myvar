package main

import (
	"bufio"
	"fmt"
	"image"
	"image/color"
	"image/draw"
	"image/png"
	"io/fs"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"golang.org/x/image/font"
	"golang.org/x/image/font/basicfont"
	"golang.org/x/image/math/fixed"
)

func main() {
	contentDir := "content"
	outputDir := "static/images"

	os.MkdirAll(outputDir, 0755)

	generateImage("MyVar.dev", filepath.Join(outputDir, "og-default.png"))

	filepath.WalkDir(contentDir, func(path string, d fs.DirEntry, err error) error {
		if err != nil || !strings.HasSuffix(path, ".md") {
			return nil
		}
		
		// Skip _index.md files
		if strings.HasSuffix(path, "_index.md") {
			return nil
		}

		title := extractTitle(path)
		if title == "" {
			return nil
		}

		relPath, _ := filepath.Rel(contentDir, path)
		imageName := strings.ReplaceAll(strings.TrimSuffix(relPath, ".md"), "/", "-") + ".png"
		outputPath := filepath.Join(outputDir, imageName)

		generateImage(title, outputPath)
		fmt.Printf("Generated: %s\n", imageName)
		return nil
	})
}

func extractTitle(filename string) string {
	file, err := os.Open(filename)
	if err != nil {
		return ""
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	titleRegex := regexp.MustCompile(`^title\s*[=:]\s*["'](.+)["']`)

	for scanner.Scan() {
		line := scanner.Text()
		if matches := titleRegex.FindStringSubmatch(line); len(matches) > 1 {
			return matches[1]
		}
	}
	return ""
}

func generateImage(title, outputPath string) {
	width, height := 1200, 630
	img := image.NewRGBA(image.Rect(0, 0, width, height))

	draw.Draw(img, img.Bounds(), &image.Uniform{color.White}, image.Point{}, draw.Src)

	face := basicfont.Face7x13
	drawer := &font.Drawer{
		Dst:  img,
		Src:  image.NewUniform(color.Black),
		Face: face,
	}

	textWidth := drawer.MeasureString(title)
	x := (fixed.I(width) - textWidth) / 2
	y := fixed.I(height / 2)

	drawer.Dot = fixed.Point26_6{X: x, Y: y}
	drawer.DrawString(title)

	file, err := os.Create(outputPath)
	if err != nil {
		fmt.Printf("Error creating %s: %v\n", outputPath, err)
		return
	}
	defer file.Close()

	png.Encode(file, img)
}