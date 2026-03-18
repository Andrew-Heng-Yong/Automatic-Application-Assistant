Workflow

1. Check page ready  
   1. Check if ww.png exists, go to step2  
2. Find the job that is:  
   1. Unapplied: apply.png exists in that row  
   2. Correct level: row contains jr.png or Inter.png(can be changed later)  
   3. Highest row(first option) that fits these conditions  
   4. Scroll down if needed  
   5. If none find, return “no jobs aval”  
3. Apply:  
   1. Click: apply.png  
      1. If no action after a few tries, stop the program and say “apply button error”  
   2. Expected to be directed to one of two page:   
      1. If psq.png is detected, go to step 4  
      2. If app\_option.png is detected, go to step 5  
4. Prescreening questions:  
   1. Wait for user to finish answering pre-screening questions  
   2. When app\_option.png has been detected, proceed to next step  
5. Write cover letter and :  
   1. click quickview.png  
   2. Copy text: from “Job \- Country:” all the way to the front of “Targeted Degrees and Disciplines:”, and Find and update company name: it can be found between “Organization:” and “Division:” 
   3. Click close.png, wait 0.5 second, click the same position again(warning: do not attempt to click close.png, it does not exist, however clicking the position where close.png was is able to deselect stuff).   
   4. Send job description to:  
      1. if current company name \= prev company name, send it to def generate\_cover\_letter\_minor\_change(job\_description: str, prev\_cover\_letter\_pdf: str | Path,) \-\> tuple\[str, str\]: resume version name, cover letter file name  
      2. Else, send it to def generate\_cover\_letter(job\_description: str) \-\> tuple\[str, str\]: resume version name, cover letter file name  
   5. Store and update resume version name and last cover letter filename   
6. apply:  
   1. Click create\_custome\_package.png  
   2. Scroll to bottom of page  
   3. Upload the cover letter:  
      1. Click upload\_new\_cover\_letter.png  
      2. Click text\_bar.png  
      3. Paste cover letter filename  
      4. Click upload.png  
      5. Click choose\_file.png  
      6. Find the file in file explorer select first pdf file by clicking on the top pdf.png  
      7. Click open.png, wait 2 second  
      8. Click upload\_document.png  
   4. Click the corresponding resume based on the resume version name, there will conveniently be a few png named by the resume version. Can be edited later  
   5. Click submit.png  
7. Finish  
   1. If confirm.png is detected, click done.png  
   2. The tab will be automatically closed, go back to step 2

Additional information:

* Save cover letter in generated\_cover\_letter/  
* Deprecate pdf saving ability in main.py