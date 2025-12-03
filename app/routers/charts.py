from fastapi import APIRouter, HTTPException, Response
from io import BytesIO

from reportlab.pdfgen import canvas   
from reportlab.lib.pagesizes import A4, landscape

from app.schemas.natal import NatalRequest
from app.schemas.synastry import SynastryRequest
from app.schemas.transit import TransitRequest
from app.schemas.composite import CompositeRequest
from app.services.chart_generator import (
    generate_natal_chart,
    generate_synastry_chart,
    generate_transit_chart,
    generate_composite_chart,
)

from app.services.pdf.wheel_page import draw_wheel_page
from app.services.pdf.natal_report import draw_natal_report_body


router = APIRouter(tags=["charts"])


@router.post("/natal", summary="Generate natal chart with SVG")
async def natal_endpoint(req: NatalRequest):
    try:
        return generate_natal_chart(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Natal chart generation failed: {e}")
    
    
@router.post("/natal/pdf", summary="Generate natal chart PDF (wheel + report)")
async def natal_pdf_endpoint(req: NatalRequest):
    try:
        # 1. Use your existing generator
        result = generate_natal_chart(req)
        svg_string = result["svg"]
        data = result["data"]  # whatever you want in the body

        # 2. Create PDF buffer
        buffer = BytesIO()

        # PAGE 1: wheel (landscape)
        c = canvas.Canvas(buffer, pagesize=landscape(A4))
        draw_wheel_page(c, svg_string)
        c.showPage()

        # PAGE 2+: report body (portrait)
        c.setPageSize(A4)
        draw_natal_report_body(c, data, req)  # you'll define this helper just below
        c.showPage()

        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return Response(content=pdf_bytes, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Natal PDF generation failed: {e}")


@router.post("/synastry", summary="Generate synastry chart with SVG")
async def synastry_endpoint(req: SynastryRequest):
    try:
        return generate_synastry_chart(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synastry chart generation failed: {e}")
    
    
@router.post("/synastry/pdf", summary="Generate synastry chart PDF (wheel + report)")
async def synastry_pdf_endpoint(req: SynastryRequest):
    try:
        result = generate_synastry_chart(req)
        svg_string = result["svg"]
        data = result["data"]

        buffer = BytesIO()

        # PAGE 1: wheel (landscape)
        c = canvas.Canvas(buffer, pagesize=landscape(A4))
        draw_wheel_page(c, svg_string)
        c.showPage()

        # PAGE 2+: report body (portrait)
        c.setPageSize(A4)
        draw_synastry_report_body(c, data, req)
        c.showPage()

        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return Response(content=pdf_bytes, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synastry PDF generation failed: {e}")


@router.post("/transit", summary="Generate transit chart with SVG")
async def transit_endpoint(req: TransitRequest):
    try:
        return generate_transit_chart(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transit chart generation failed: {e}")
    
    
@router.post("/transit/pdf", summary="Generate transit chart PDF (wheel + report)")
async def transit_pdf_endpoint(req: TransitRequest):
    try:
        result = generate_transit_chart(req)
        svg_string = result["svg"]
        data = result["data"]

        buffer = BytesIO()

        c = canvas.Canvas(buffer, pagesize=landscape(A4))
        draw_wheel_page(c, svg_string)
        c.showPage()

        c.setPageSize(A4)
        draw_transit_report_body(c, data, req)
        c.showPage()

        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return Response(content=pdf_bytes, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transit PDF generation failed: {e}")


@router.post("/composite", summary="Generate composite chart with SVG")
async def composite_endpoint(req: CompositeRequest):
    try:
        return generate_composite_chart(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Composite chart generation failed: {e}")
    
    
@router.post("/composite/pdf", summary="Generate composite chart PDF (wheel + report)")
async def composite_pdf_endpoint(req: CompositeRequest):
    try:
        result = generate_composite_chart(req)
        svg_string = result["svg"]
        data = result["data"]

        buffer = BytesIO()

        c = canvas.Canvas(buffer, pagesize=landscape(A4))
        draw_wheel_page(c, svg_string)
        c.showPage()

        c.setPageSize(A4)
        draw_composite_report_body(c, data, req)
        c.showPage()

        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return Response(content=pdf_bytes, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Composite PDF generation failed: {e}")
    

    