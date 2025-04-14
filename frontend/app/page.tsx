'use client';

import HeaderNav from '@/components/HeaderNav';
import QueryInterface from '@/components/QueryInterface';
import { Box } from '@chakra-ui/react';

export default function Page() {
  return (
    <Box minH="100vh" bg="#F5F5F7">
      <HeaderNav signOut={() => {}} />
      <QueryInterface />
    </Box>
  );
}
