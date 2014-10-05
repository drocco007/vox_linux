# ∅MQ multi-publisher message bus
#
# modeled on http://zguide.zeromq.org/py:msgqueue but with XPUB/XSUB instead
# of ROUTER/DEALER
#
# usage: julia bus.jl <publisher_port> <subscriber_port>
#

using ZMQ

context = Context(1)

bus_in = Socket(context, ZMQ.XSUB)
bus_out = Socket(context, ZMQ.XPUB)

ZMQ.bind(bus_in, "tcp://*:$(ARGS[1])")
ZMQ.bind(bus_out, "tcp://*:$(ARGS[2])")

println("∅MQ multi-publisher message bus $(ARGS[1])→$(ARGS[2])")

# zmq_device(FORWARDER, bus_in, bus_out)
ccall( (:zmq_device, "libzmq"), Int64, (Int64, Socket, Socket),
	FORWARDER, bus_in, bus_out)

# shouldn't get here
ZMQ.close(bus_in)
ZMQ.close(bus_out)
ZMQ.close(context)
