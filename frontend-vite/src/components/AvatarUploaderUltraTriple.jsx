import { useRef, useState, useEffect } from "react"

export default function AvatarUploaderUltraTriple({ personId }) {

  const inputRef = useRef(null)
  const canvasRef = useRef(null)

  const [img,setImg] = useState(null)
  const [zoom,setZoom] = useState(1)
  const [rotation,setRotation] = useState(0)
  const [pos,setPos] = useState({x:0,y:0})
  const [dragging,setDragging] = useState(false)
  const [start,setStart] = useState({x:0,y:0})
  const [reload,setReload] = useState(0)

  const uploadLock = useRef(false)

  const avatarUrl =
    `http://localhost:8010/cdn/avatar/${personId}?v=${reload}`

  const fallback="/default-avatar.png"


  // ===============================
  // LOAD CURRENT AVATAR
  // ===============================

  useEffect(()=>{

    const image = new Image()

    image.src = avatarUrl

    image.onload = ()=>{

      const fitZoom =
        Math.min(
          400/image.width,
          400/image.height
        )

      setZoom(fitZoom)
      setRotation(0)
      setPos({x:0,y:0})
      setImg(image)

    }

  },[avatarUrl])


  // ===============================
  // DRAW ENGINE
  // ===============================

  useEffect(()=>{

    if(!img) return

    draw(img,zoom,rotation,pos)

  },[img,zoom,rotation,pos])


  const draw=(image,z,rot,p)=>{

    const canvas=canvasRef.current
    if(!canvas) return

    const ctx=canvas.getContext("2d")

    canvas.width=400
    canvas.height=400

    ctx.clearRect(0,0,400,400)

    ctx.save()

    ctx.translate(200,200)
    ctx.rotate(rot*Math.PI/180)

    const w=image.width*z
    const h=image.height*z

    ctx.drawImage(
      image,
      -w/2 - p.x,
      -h/2 - p.y,
      w,
      h
    )

    ctx.restore()

    // circle border

    ctx.beginPath()
    ctx.arc(200,200,190,0,Math.PI*2)
    ctx.strokeStyle="#ffffff"
    ctx.lineWidth=3
    ctx.stroke()

  }



  // ===============================
  // LOAD IMAGE
  // ===============================

  const loadImage=(file)=>{

    const reader=new FileReader()

    reader.onload=e=>{

      const image=new Image()

      image.src=e.target.result

      image.onload=()=>{

        const fitZoom =
          Math.min(
            400/image.width,
            400/image.height
          )

        setZoom(fitZoom)
        setRotation(0)
        setPos({x:0,y:0})
        setImg(image)

      }
    }

    reader.readAsDataURL(file)

  }



  // ===============================
  // DRAG
  // ===============================

  const mouseDown=(e)=>{

    setDragging(true)
    setStart({x:e.clientX,y:e.clientY})

  }


  const mouseMove=(e)=>{

    if(!dragging) return

    const dx=(e.clientX-start.x)/zoom
    const dy=(e.clientY-start.y)/zoom

    const newPos={
      x:pos.x-dx,
      y:pos.y-dy
    }

    setPos(newPos)

    setStart({x:e.clientX,y:e.clientY})

  }


  const mouseUp=()=>setDragging(false)



  // ===============================
  // ZOOM
  // ===============================

  const handleZoom=(v)=>{

    setZoom(parseFloat(v))

  }



  // ===============================
  // ROTATE
  // ===============================

  const handleRotate=(deg)=>{

    setRotation(rotation+deg)

  }



  // ===============================
  // COMPRESS
  // ===============================

  const compressBlob=(canvas)=>
    new Promise(resolve=>{
      canvas.toBlob(resolve,"image/jpeg",0.82)
    })



  // ===============================
  // UPLOAD
  // ===============================

  const upload=async()=>{

    if(uploadLock.current) return

    uploadLock.current=true

    const canvas=canvasRef.current

    const blob=await compressBlob(canvas)

    const form=new FormData()

    form.append("file",blob,"avatar.jpg")

    const res = await fetch(
      `http://localhost:8010/api/person/${personId}/avatar`,
      {method:"POST",body:form}
    )

    uploadLock.current=false

    if(!res.ok){

      alert("Upload failed")
      return

    }

    setReload(Date.now())

    setImg(null)

    window.dispatchEvent(new Event("avatarUpdated"))

    alert("Avatar updated")

  }



  // ===============================
  // DROP
  // ===============================

  const handleDrop=(e)=>{

    e.preventDefault()

    const file=e.dataTransfer.files?.[0]

    if(file) loadImage(file)

  }



  // ===============================
  // RENDER
  // ===============================

  return(

    <div
      className="flex flex-col items-center gap-3"
      onDrop={handleDrop}
      onDragOver={(e)=>e.preventDefault()}
    >

      {!img && (

        <img
          src={avatarUrl}
          onError={(e)=>e.target.src=fallback}
          className="w-32 h-32 rounded-full border object-cover cursor-pointer"
          onClick={()=>inputRef.current.click()}
        />

      )}


      {img && (

        <canvas
          ref={canvasRef}
          className="border rounded-lg cursor-move"
          onMouseDown={mouseDown}
          onMouseMove={mouseMove}
          onMouseUp={mouseUp}
          onMouseLeave={mouseUp}
        />

      )}


      <input
        type="file"
        hidden
        ref={inputRef}
        accept="image/*"
        onChange={(e)=>loadImage(e.target.files[0])}
      />


      {img && (

        <>

          <div className="flex gap-2">

            <button
              onClick={()=>handleRotate(-90)}
              className="px-2 py-1 bg-gray-200 rounded"
            >
              ↺
            </button>

            <button
              onClick={()=>handleRotate(90)}
              className="px-2 py-1 bg-gray-200 rounded"
            >
              ↻
            </button>

          </div>


          <input
            type="range"
            min="0.1"
            max="3"
            step="0.01"
            value={zoom}
            onChange={(e)=>handleZoom(e.target.value)}
          />


          <button
            onClick={upload}
            className="px-4 py-1 bg-green-600 text-white rounded"
          >
            Upload Avatar
          </button>

        </>

      )}

      <p className="text-xs text-gray-500">
        Click hoặc kéo ảnh vào – kéo chuột để crop
      </p>

    </div>

  )

}