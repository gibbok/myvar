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

	"github.com/golang/freetype"
	"github.com/golang/freetype/truetype"
	"golang.org/x/image/font/gofont/goregular"
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

	// Parse font
	f, err := truetype.Parse(goregular.TTF)
	if err != nil {
		fmt.Printf("Error parsing font: %v\n", err)
		return
	}

	// Create freetype context with antialiasing
	c := freetype.NewContext()
	c.SetDPI(72)
	c.SetFont(f)
	c.SetFontSize(40)
	c.SetClip(img.Bounds())
	c.SetDst(img)
	c.SetSrc(image.NewUniform(color.Black))

	// Wrap text if too long
	maxWidth := width - 120 // 60px padding on each side
	lines := wrapText(title, maxWidth, c)
	
	// Calculate starting Y position for multiple lines
	lineHeight := c.PointToFixed(40)
	totalHeight := lineHeight * fixed.Int26_6(len(lines)-1)
	startY := fixed.I(height/2) - totalHeight/2
	
	// Draw each line centered
	for i, line := range lines {
		textWidth := c.PointToFixed(40) * fixed.Int26_6(len(line)) / 2
		x := (fixed.I(width) - textWidth) / 2
		y := startY + lineHeight*fixed.Int26_6(i)
		
		pt := fixed.Point26_6{X: x, Y: y}
		c.DrawString(line, pt)
	}

	file, err := os.Create(outputPath)
	if err != nil {
		fmt.Printf("Error creating %s: %v\n", outputPath, err)
		return
	}
	defer file.Close()

	png.Encode(file, img)
}

func wrapText(text string, maxWidth int, c *freetype.Context) []string {
	words := strings.Fields(text)
	if len(words) == 0 {
		return []string{text}
	}
	
	var lines []string
	currentLine := ""
	
	for _, word := range words {
		testLine := currentLine
		if testLine != "" {
			testLine += " "
		}
		testLine += word
		
		// Rough estimate: 40px font ≈ 24px average character width
		estimatedWidth := len(testLine) * 24
		if estimatedWidth > maxWidth && currentLine != "" {
			lines = append(lines, currentLine)
			currentLine = word
		} else {
			currentLine = testLine
		}
	}
	
	if currentLine != "" {
		lines = append(lines, currentLine)
	}
	
	return lines
}