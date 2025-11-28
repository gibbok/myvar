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
	"golang.org/x/image/font/gofont/gobold"
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
	
	// Create horizontal gradient background from #cb2a42 to #adadad
	img := image.NewRGBA(image.Rect(0, 0, width, height))
	leftColor := color.RGBA{0xcb, 0x2a, 0x42, 0xff}
	rightColor := color.RGBA{0xad, 0xad, 0xad, 0xff}
	
	for x := 0; x < width; x++ {
		// Calculate interpolation factor (0.0 to 1.0)
		t := float64(x) / float64(width-1)
		
		// Interpolate RGB values
		r := uint8(float64(leftColor.R)*(1-t) + float64(rightColor.R)*t)
		g := uint8(float64(leftColor.G)*(1-t) + float64(rightColor.G)*t)
		b := uint8(float64(leftColor.B)*(1-t) + float64(rightColor.B)*t)
		
		c := color.RGBA{r, g, b, 0xff}
		for y := 0; y < height; y++ {
			img.Set(x, y, c)
		}
	}

	// Parse font
	f, err := truetype.Parse(gobold.TTF)
	if err != nil {
		fmt.Printf("Error parsing font: %v\n", err)
		return
	}

	// Create freetype context with antialiasing
	c := freetype.NewContext()
	c.SetDPI(300)
	c.SetFont(f)
	c.SetFontSize(24)
	c.SetClip(img.Bounds())
	c.SetDst(img)
	c.SetSrc(image.NewUniform(color.White))

	// Wrap text if too long
	maxWidth := width - 80 // 40px padding on each side
	lines := wrapText(title, maxWidth, c)
	
	// Calculate starting Y position for multiple lines
	fontSize := 24.0
	lineHeight := c.PointToFixed(fontSize * 1.2) // 1.2x font size for line height
	margin := 40
	startY := fixed.I(margin) + lineHeight
	
	// Draw each line aligned to top-left
	boldOffset := fixed.Int26_6(32)
	for i, line := range lines {
		x := fixed.I(margin)
		y := startY + lineHeight*fixed.Int26_6(i)
		
		// Draw text multiple times with offsets for extra bold effect
		for dx := fixed.Int26_6(0); dx <= boldOffset; dx += 32 {
			for dy := fixed.Int26_6(0); dy <= boldOffset; dy += 32 {
				pt := fixed.Point26_6{X: x + dx, Y: y + dy}
				c.DrawString(line, pt)
			}
		}
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
	
	f, _ := truetype.Parse(gobold.TTF)
	face := truetype.NewFace(f, &truetype.Options{
		Size: 24,
		DPI:  300,
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