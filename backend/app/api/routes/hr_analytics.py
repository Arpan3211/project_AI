from typing import List, Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Handle imports for both direct and package execution
try:
    from app.db.database import get_db
    from app.services.auth import get_current_user
    from app.services.hr_analytics import process_hr_analytics_query
    from app.schemas.hr_analytics import HRAnalyticsQuery, HRAnalyticsResponse
    from app.models.user import User
except ImportError:
    from backend.app.db.database import get_db
    from backend.app.services.auth import get_current_user
    from backend.app.services.hr_analytics import process_hr_analytics_query
    from backend.app.schemas.hr_analytics import HRAnalyticsQuery, HRAnalyticsResponse
    from backend.app.models.user import User

router = APIRouter()

@router.post("/hr-analytics/query", response_model=HRAnalyticsResponse)
def query_hr_analytics(
    query_in: HRAnalyticsQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Process an HR analytics query with conversation history.
    """
    try:
        # Process the query
        response = process_hr_analytics_query(
            query=query_in.query,
            conversation_history=query_in.conversation_history
        )
        
        # Return the response
        return HRAnalyticsResponse(
            answer=response.get("answer", ""),
            query=response.get("query", ""),
            result=response.get("result", ""),
            analysis=response.get("analysis", "")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing HR analytics query: {str(e)}"
        )
