0.  Alex Modzelewski (am2408)
    Shadmehr Khan (srk169)

1.  There were many issues with the code. The receieve_packets function would mostly work but the WND for the last
ACK was off by a bit, likely due to the WND not being reset properly. The data and ACKs were otherwise correctly placed into the output files.

2.  The only individuals that worked on this project are those listed under number 0. The references used were as follows:
        "The TCP/IP Guide" on tcpipguide.com
        "Transmission Control Protocol" on wikipedia.com
        "RFC 791 : Transmission Control Protocol" on datatracker.org
        "RFC 5681 : TCP Congestion Control" on rfc-editor.org 
        "RFC 9293 : Transmission Control Protocol (TCP)" on rfc-editor.org
        "RFC 6298 : Computing TCP's Retransmission Timer" on rfc-editor.org
        "Lecture 7 transport layer" on Canvas
        Various online lectures 

3.  The main issue with this project is the scope of it. There is far too much to code in just two weeks; it would be too much even in a
month-time. Understanding the provided code took multiple hours of a few days, and then there were about 4-6 hours spent each day including a 
3-day extension. The time constraints were made even more difficult with studying for a midterm for this class as well as another, homeworks
and assignments due for both, a project for the other course, and work during the day as well. A large part of this project was spent looking
at either the lecture notes on TCP or the RFC as well as combing through the provided code to figure out what aspects are already integrated
into the code and what we had to code ourselves.