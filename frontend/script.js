let transcriptText = ""

const transcriptInput = document.getElementById("transcriptFile")
const audioInput = document.getElementById("audioFile")

const uploadTranscriptBtn = document.getElementById("uploadTranscriptBtn")
const uploadAudioBtn = document.getElementById("uploadAudioBtn")
const analyzeBtn = document.getElementById("analyzeBtn")

const summaryBox = document.getElementById("summaryBox")
const tasksContainer = document.getElementById("tasksContainer")


/* Upload transcript */

uploadTranscriptBtn.onclick = () => {
transcriptInput.click()
}

transcriptInput.onchange = async () => {

const file = transcriptInput.files[0]

if(!file){
alert("Select transcript file")
return
}

const text = await file.text()

transcriptText = text

alert("Transcript uploaded successfully")
}


/* Upload audio */

uploadAudioBtn.onclick = () => {
audioInput.click()
}

audioInput.onchange = async () => {

const file = audioInput.files[0]

if(!file){
alert("Select audio file")
return
}

const formData = new FormData()
formData.append("audio", file)

const res = await fetch("/upload-audio",{
method:"POST",
body:formData
})

const data = await res.json()

if(data.error){
alert(data.error)
return
}

/* store transcript returned */
transcriptText = data.transcript

showSummary(data.summary)
showTasks(data.tasks)

alert("Audio processed successfully")

}


/* Analyze meeting */

analyzeBtn.onclick = async () => {

if(!transcriptText){
alert("Upload transcript or audio first")
return
}

const res = await fetch("/process-text",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
transcript: transcriptText
})
})

const data = await res.json()

if(data.error){
alert(data.error)
return
}

showSummary(data.summary)
showTasks(data.tasks)

}


/* Show summary */

function showSummary(summary){

summaryBox.innerHTML=""

/* handle empty summary */

if(!summary){
summaryBox.innerHTML="<p>No summary generated</p>"
return
}

/* FIX: if summary is string convert to array */

if(typeof summary === "string"){
summary = summary.split(".")
}

/* ensure summary is array */

if(!Array.isArray(summary)){
summary = [summary]
}

summary.forEach(point => {

if(point.trim()==="") return

const p=document.createElement("p")
p.innerText="• "+point.trim()

summaryBox.appendChild(p)

})

}


/* Show tasks */

function showTasks(tasks){

tasksContainer.innerHTML=""

if(!tasks) return

tasks.forEach(task => {

const div=document.createElement("div")
div.className="task-card"

div.innerHTML=`
<h3>${task.title}</h3>
<p>${task.description}</p>

<div class="tags">
<span class="priority">${task.priority}</span>
<span class="category">${task.category}</span>
<span class="status">${task.status}</span>
</div>

<button class="issueBtn">Open GitHub Issue</button>
`

div.querySelector("button").onclick=async()=>{

const repo=document.getElementById("repo").value
const token=document.getElementById("token").value

const res=await fetch("/create-issue",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
repo:repo,
token:token,
task:task
})
})

const issue=await res.json()

const url = issue.html_url || issue.url

if(url){
window.open(url,"_blank")
}else{
alert("Issue created but link unavailable")
}

}

tasksContainer.appendChild(div)

})

}