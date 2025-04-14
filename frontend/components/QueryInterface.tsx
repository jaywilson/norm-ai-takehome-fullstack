'use client';

import { useState } from 'react';
import {
  Box,
  Button,
  Container,
  Flex,
  Input,
  Text,
  VStack,
  Divider,
  Heading,
  List,
  ListItem,
  Badge,
  FormControl,
  FormLabel,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  HStack,
} from '@chakra-ui/react';

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

export default function QueryInterface() {
  const [query, setQuery] = useState('');
  const [topK, setTopK] = useState<number>(3);
  const [response, setResponse] = useState<string>('');
  const [citations, setCitations] = useState<Citation[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    setCitations([]);
    
    try {
      // Create URL with query parameter to our Next.js API route
      const url = new URL('/api/query', window.location.origin);
      url.searchParams.append('query', query);
      url.searchParams.append('top_k', topK.toString());
      
      const res = await fetch(url.toString(), {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }
      
      const data: QueryResponse = await res.json();
      setResponse(data.response);
      
      // Set citations if they exist in the response
      if (data.citations && Array.isArray(data.citations)) {
        setCitations(data.citations);
      }
    } catch (error) {
      console.error('Error fetching response:', error);
      setResponse('An error occurred while processing your request.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.md" py={8}>
      <VStack spacing={6} align="stretch">
        <HStack spacing={4} align="flex-end">
          <Box flex="1">
            <FormControl>
              <FormLabel>Enter your query:</FormLabel>
              <Input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Type your question here..."
                size="md"
                onKeyPress={(e) => {
                  if (e.key === 'Enter') handleSubmit();
                }}
              />
            </FormControl>
          </Box>
          
          <Box width="100px">
            <FormControl>
              <FormLabel>Top K:</FormLabel>
              <NumberInput 
                min={1} 
                max={20} 
                value={topK} 
                onChange={(valueString) => setTopK(parseInt(valueString))}
              >
                <NumberInputField />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
            </FormControl>
          </Box>
          
          <Button
            colorScheme="blue"
            onClick={handleSubmit}
            isLoading={isLoading}
            loadingText="Sending"
            bg="#2800D7"
            _hover={{ bg: '#3810E7' }}
            height="40px"
          >
            Send
          </Button>
        </HStack>

        {response && (
          <Box
            borderWidth="1px"
            borderRadius="md"
            p={4}
            bg="white"
            borderColor="#DBDCE1"
            minH="200px"
          >
            <Text fontWeight="medium" mb={2}>Response:</Text>
            <Text mb={4}>{response}</Text>
            
            {citations.length > 0 && (
              <>
                <Divider my={4} />
                <Heading as="h3" size="sm" mb={3}>
                  Citations
                </Heading>
                <List spacing={3}>
                  {citations.map((citation, index) => (
                    <ListItem key={index} pb={2} borderBottom="1px solid #DBDCE1">
                      <Flex mb={1}>
                        <Badge colorScheme="blue" mr={2}>
                          {index + 1}
                        </Badge>
                        <Text fontWeight="medium">
                          {citation.source}
                        </Text>
                      </Flex>
                      <Text pl={6} fontSize="sm" color="gray.700">
                        {citation.text}
                      </Text>
                    </ListItem>
                  ))}
                </List>
              </>
            )}
          </Box>
        )}
      </VStack>
    </Container>
  );
}