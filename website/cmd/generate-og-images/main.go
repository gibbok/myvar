package main

import (
	"bufio"
	"fmt"
	"image"
	"image/color"
	"image/png"
	"io/fs"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/golang/freetype"
	"github.com/golang/freetype/truetype"
	"golang.org/x/image/font"
	"golang.org/x/image/font/gofont/gomedium"
	"golang.org/x/image/math/fixed"
)

const (
	contentDir = "content"
	outputDir  = "static/images"
	imageWidth = 1200
	imageHeight = 630
	fontSize = 6.0
	fontDPI = 1200
	topMargin = 15
	leftMargin = 35
)

func main() {
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		fmt.Printf("Error creating output directory: %v\n", err)
		return
	}

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
	// Create horizontal gradient background
	img := image.NewRGBA(image.Rect(0, 0, imageWidth, imageHeight))
	leftColor := color.RGBA{0xcb, 0x2a, 0x42, 0xff}
	rightColor := color.RGBA{0xa0, 0x35, 0x35, 0xff}
	
	for x := 0; x < imageWidth; x++ {
		t := float64(x) / float64(imageWidth-1)
		
		// Interpolate RGB values
		r := uint8(float64(leftColor.R)*(1-t) + float64(rightColor.R)*t)
		g := uint8(float64(leftColor.G)*(1-t) + float64(rightColor.G)*t)
		b := uint8(float64(leftColor.B)*(1-t) + float64(rightColor.B)*t)
		
		c := color.RGBA{r, g, b, 0xff}
		for y := 0; y < imageHeight; y++ {
			img.Set(x, y, c)
		}
	}

	// Parse font
	f, err := truetype.Parse(gomedium.TTF)
	if err != nil {
		fmt.Printf("Error parsing font: %v\n", err)
		return
	}

	// Create freetype context
	c := freetype.NewContext()
	c.SetDPI(fontDPI)
	c.SetFont(f)
	c.SetFontSize(fontSize)
	c.SetClip(img.Bounds())
	c.SetDst(img)
	c.SetSrc(image.NewUniform(color.White))

	// Wrap text
	maxWidth := imageWidth - (leftMargin * 2)
	lines := wrapText(title, maxWidth, f)
	
	// Calculate starting Y position
	lineHeight := c.PointToFixed(fontSize * 1.2)
	startY := fixed.I(topMargin) + lineHeight
	
	// Draw each line aligned to top-left
	for i, line := range lines {
		x := fixed.I(leftMargin)
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

func wrapText(text string, maxWidth int, f *truetype.Font) []string {
	words := strings.Fields(text)
	if len(words) == 0 {
		return []string{text}
	}
	
	face := truetype.NewFace(f, &truetype.Options{
		Size: fontSize,
		DPI:  fontDPI,
	})
	
	var lines []string
	currentLine := ""
	
	for _, word := range words {
		testLine := currentLine
		if testLine != "" {
			testLine += " "
		}
		testLine += word
		
		textWidth := font.MeasureString(face, testLine)
		actualWidth := int(textWidth >> 6)
		
		if actualWidth > maxWidth && currentLine != "" {
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