import { useRef, useState } from "react"

export default function AvatarUploaderUltraTriple({ personId }) {

  const inputRef = useRef(null)
  const canvasRef = useRef(null)

  const [img,setImg] = useState(null)
  const [zoom,setZoom] = useState(1)
  const [rotation,setRotation] = useState(0)
  const [pos,setPos] = useState({x:0,y:0})
  const [dragging,setDragging] = useState(false)
  const [start,setStart] = useState({x:0,y:0})

  const uploadLock = useRef(false)

  const avatarUrl =
    `http://localhost:8010/cdn/avatar/${personId}?t=${Date.now()}`

  const fallback="/default-avatar.png"

  // --------------------------------------------------
  // LOAD IMAGE
  // --------------------------------------------------

  const loadImage=(file)=>{

    const reader=new FileReader()

    reader.onload=e=>{

      const image=new Image()
      image.src=e.target.result

      image.onload=()=>{

        const autoPos = autoFaceCenter(image)

        setImg(image)
        setPos(autoPos)

        draw(image,zoom,rotation,autoPos)
      }
    }

    reader.readAsDataURL(file)
  }

  // --------------------------------------------------
  // FACE CENTER
  // --------------------------------------------------

  const autoFaceCenter=(image)=>{

    const cx=image.width/2
    const cy=image.height*0.35

    return {
      x:cx/4,
      y:cy/4
    }
  }

  // --------------------------------------------------
  // DRAW
  // --------------------------------------------------

  const draw=(image,z,rot,p)=>{

    const canvas=canvasRef.current
    const ctx=canvas.getContext("2d")

    canvas.width=400
    canvas.height=400

    ctx.clearRect(0,0,400,400)

    ctx.save()

    ctx.translate(200,200)
    ctx.rotate(rot*Math.PI/180)

    const size=Math.min(image.width,image.height)

    ctx.drawImage(
      image,
      -size*z/2 - p.x,
      -size*z/2 - p.y,
      size*z,
      size*z
    )

    ctx.restore()

    ctx.beginPath()
    ctx.arc(200,200,190,0,Math.PI*2)
    ctx.strokeStyle="#ddd"
    ctx.lineWidth=3
    ctx.stroke()
  }

  // --------------------------------------------------
  // ZOOM
  // --------------------------------------------------

  const handleZoom=(v)=>{

    const z=parseFloat(v)

    setZoom(z)

    if(img) draw(img,z,rotation,pos)
  }

  // --------------------------------------------------
  // ROTATE
  // --------------------------------------------------

  const handleRotate=(deg)=>{

    const r=rotation+deg

    setRotation(r)

    if(img) draw(img,zoom,r,pos)
  }

  // --------------------------------------------------
  // DRAG
  // --------------------------------------------------

  const mouseDown=(e)=>{
    setDragging(true)
    setStart({x:e.clientX,y:e.clientY})
  }

  const mouseMove=(e)=>{

    if(!dragging) return

    const dx=e.clientX-start.x
    const dy=e.clientY-start.y

    const newPos={
      x:pos.x-dx,
      y:pos.y-dy
    }

    setPos(newPos)
    setStart({x:e.clientX,y:e.clientY})

    if(img) draw(img,zoom,rotation,newPos)
  }

  const mouseUp=()=>setDragging(false)

  // --------------------------------------------------
  // COMPRESS
  // --------------------------------------------------

  const compressBlob=(canvas)=>
    new Promise(resolve=>{
      canvas.toBlob(resolve,"image/jpeg",0.82)
    })

  // --------------------------------------------------
  // UPLOAD
  // --------------------------------------------------

  const upload=async()=>{

    if(uploadLock.current) return

    uploadLock.current=true

    const canvas=canvasRef.current

    const blob=await compressBlob(canvas)

    const form=new FormData()

    form.append("file",blob,"avatar.jpg")

    await fetch(
        `http://localhost:8010/api/tree/avatar/${personId}`,
        {method:"POST",body:form}
    )

    uploadLock.current=false

    // force reload avatar everywhere

    window.dispatchEvent(new Event("avatarUpdated"))

    alert("Avatar updated")
  }

  // --------------------------------------------------
  // DROP
  // --------------------------------------------------

  const handleDrop=(e)=>{

    e.preventDefault()

    const file=e.dataTransfer.files[0]

    if(file) loadImage(file)
  }

  // --------------------------------------------------
  // RENDER
  // --------------------------------------------------

  return (

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
            min="1"
            max="2"
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