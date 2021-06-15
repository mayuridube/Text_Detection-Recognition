# Text_Recognition_using_tesserocr
<H4> Installation Guide </h4>
1.Follow installation_guide.txt in repo<br>

<h4> Usage:</h4>
1.Only print the text from image<br>
$ python3 main.py --image './images/5.png'<br>

2.Print the each word from image with its confidence<br>
$ python3 main.py --image './images/5.png' --confidence True<br>

<h4> Outputs: </h4>
<p>
 <h5> 1.straight image </h5><br>
 <img src="images/5.png", height="100",width="80"></img> <img src="images/op_5.png", height="100",width="80"></img>
</p>

<p>
 <h3> 2.blur image </h3><br>
 <img src="images/3.jpeg"></img>
 <h2>Output:Image is Blur,unable to get OCR.</h2>
</p>

<p>
 <h3> 3.Rotated image </h3><br>
 <img src="images/1.jpg"></img>
 <img src="images/op_1.png"></img>
</p>
