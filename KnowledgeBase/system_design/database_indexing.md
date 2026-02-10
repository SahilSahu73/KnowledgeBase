Database is a collection of records, which needs to be serialized and stored in the disk.

We have a table with 5 columns:
Id - 4B
name - 60B
age - 4B
bio - 128B
total_blogs - 4B

Therefore, Each record in the Users table will be 200B long.
So if the table has 100 rows then the total size of the table will be 20000B.

## How reads from the disk actually happen?
To do any read operation from the disk, we don't only read the particular byte that we want
but we read the entire block in which our content is.

The disk (HDD,SSD etc.) are split into blocks.
The blocks are consecutive in nature, and the standard block size is 4KB.

So when we do a disk IO operation, we go to the disk, fetch the block which contains our
requested bytes, and load the block into the memory, and then read it from there and send
for further processing.
Block is the unit of data read from the disk.

How does the table rows then fit into the blocks?
We know that each row takes 200B of space.
And for example lets assume that each block is of 600B.
Therefore in each block we can store 3 rows/records.

The entire Users table having 100 rows can fit in 100/3 = 33.3 ~ 34 blocks.
So reading the entire table will require the DB engine to read 34 blocks from the disk.

To read the table we would have to iterate through it row by row, request a particular row,
then the CPU will receive the instruction saying that I want to read this particular row from
the disk, then it would find the byte offset, go onto the disk, read that block and load into
the memory, and then retrieve the requested row.

So the amount of time required to go through the entire table = the amount of time required
to read those many blocks from the disk.

## What is indexing?
Index is a data structure that we build and assign on top of an existing table
In real life indexing is done using bTrees 

For example and understanding purposes:
If the table does not have indexing and we want to execute a query like, find all users with 
age == 23.
In such a case the flow will be:
 - iterate table row by row -> block by block
 - read the block in memory
 - check if age==23 on each record.
 - if yes, add the record to an output buffer.
 - if no, discard
 - return the output buffer.

Time taken to answer this query is same as time taken to read the blocks.
34 blocks = 34 seconds (assuming that reading each block takes 1 second.)

### how indexing makes this faster:
indexes -> they are smaller referential tables that holds row references against the 
indexed values. (on a very high level.)
Example: say we create an index on column 'age'.
So we will have the age column ordered by the indexed value.

| age | id  |
| --- | --- |
| 21  | 2   |
| 22  | 3   |
| 22  | 5   |
| 23  | 1   |
| 23  | 4   |
| ... | ... |

So we have the age column sorted and then serialized and stored into the disk.
Each entry of the index is 4B (age) + 4B (id) = 8B
Since there are 100 entries, therefore total size of the index will be = 800B
Also since 1 block is 600B, so indexing will require only 2 blocks on the disk.

Now we will evaluate the same query with index:
 - iterate index (worst case complete index) -> block by block
 - check age == 23 in entries.
 - if yes, add the 'id' in a buffer.
 - if no, discard
 - for all the relevant id's in the buffer
    - read the records from the disk.
    - add to an output buffer
 - return the output buffer

So we first read the indexes, i.e. go through them sequentially -> worst case = read all index
blocks, in this case 2 blocks.
Blocks read = 2
This will return a list (or something of this sort) of indexes that will 

