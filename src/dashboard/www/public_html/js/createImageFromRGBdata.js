export function hexToRGB(hexStr) {
    var col = {};
    col.r = parseInt(hexStr.substr(1, 2), 16);
    col.g = parseInt(hexStr.substr(3, 2), 16);
    col.b = parseInt(hexStr.substr(5, 2), 16);
    return col;
}

function newEl(tag){return document.createElement(tag);}
export function createImageFromRGBdata(r, g, b, width, height)
{
	var mCanvas = newEl('canvas');
	mCanvas.width = width;
	mCanvas.height = height;
	
	var mContext = mCanvas.getContext('2d');
	var mImgData = mContext.createImageData(width, height);
	
	var srcIndex=0, dstIndex=0, curPixelNum=0;
	
	for (curPixelNum=0; curPixelNum<width*height;  curPixelNum++)
	{
		mImgData.data[dstIndex] = r;		// r
		mImgData.data[dstIndex+1] = g;	// g
		mImgData.data[dstIndex+2] = b;	// b
		mImgData.data[dstIndex+3] = 255; // 255 = 0xFF - constant alpha, 100% opaque
		srcIndex += 3;
		dstIndex += 4;
	}
	mContext.putImageData(mImgData, 0, 0);
	return mCanvas;
}