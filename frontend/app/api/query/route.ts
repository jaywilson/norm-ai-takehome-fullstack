import { NextRequest, NextResponse } from 'next/server';

// Define the Citation type
interface Citation {
  source: string;
  text: string;
}

// Define the response type
interface QueryResponse {
  response: string;
  citations?: Citation[];
}

export async function GET(request: NextRequest) {
  try {
    // Get the parameters from the request
    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get('query');
    const topK = searchParams.get('top_k') || '3'; // Default to 3 if not provided

    if (!query) {
      return NextResponse.json(
        { error: 'Query parameter is required' },
        { status: 400 }
      );
    }

    // Forward the request to the backend service
    const backendURL = new URL('http://localhost:9001/api/query');
    backendURL.searchParams.append('query', query);
    backendURL.searchParams.append('top_k', topK);

    const response = await fetch(backendURL.toString(), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.text();
      console.error(`Backend service error: ${response.status}`, errorData);
      return NextResponse.json(
        { error: 'Error from backend service' },
        { status: response.status }
      );
    }

    // Get the response from the backend and return it
    const data = await response.json();
    
    // Ensure the response format matches what our frontend expects
    const formattedResponse: QueryResponse = {
      response: data.response || '',
      citations: data.citations || []
    };
    
    return NextResponse.json(formattedResponse);
  } catch (error) {
    console.error('Error in API route:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}