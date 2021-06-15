# Text_Recognition_using_tesserocr
<H4> Installation Guide </h4>
1.Follow installation_guide.txt in repo<br>

<h4> Usage:</h4>
1.Only print the text from image<br>
$ python3 main.py --image './images/aadhar_demo2.jpg'<br>

2.Print the each word from image with its confidence<br>
$ python3 main.py --image './images/aadhar_demo2.jpg' --confidence True<br>

<h4> Outputs </h4>
<p>
 <h3> 1.straight image </h3><br>
 <img src="images/5.png"></img>
 <img src="images/op_5.png"></img>
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
