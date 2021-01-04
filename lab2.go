package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"
)

func main() {

	var url string
	fmt.Print("Write url: ")
	fmt.Scanf("%s\n", &url)


	sep_url := strings.Split(url, "/")

	var file_name string
	for i:=1; file_name == "" && i < len(sep_url); i++  { file_name = sep_url[len(sep_url)-i] }
	if file_name == "" { panic("Wrong url") }

	err := DownloadFile(file_name, url)
	if err != nil {
		panic(err)
	}
	fmt.Println("Downloaded: ")
}

func DownloadFile(filepath string, url string) error{
	if !strings.Contains(filepath, ".") { filepath += ".html" }
	out, err := os.Create(filepath)
	if err != nil{
		return err
	}
	defer out.Close()
	resp, err := http.Get(url)
	if err != nil{
		return err
	}
	defer resp.Body.Close()
	var size int64
	size = 0
	var buf bytes.Buffer
	r := io.TeeReader(resp.Body, &buf)
	fmt.Println("Loading:")
	go func () { for size ==0 { fmt.Println(buf.Len(),"bytes"); time.Sleep(time.Second) } }()
	size, err = io.Copy(out, r)

	return err

}

//                                               		tests													      \\
//https://i.imgur.com/z5ZPDKe.mp4 video ~0 sec download
//https://vk.com/video-140856686_456239570 video ~0 sec download
//https://i.pinimg.com/564x/01/64/26/016426ebe7bcab81db7a03fc2329cde5.jpg ~0 sec download
//https://m1.ppy.sh/r/osu!install.exe ~2 sec :)
