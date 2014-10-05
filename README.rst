==============
 Dragon Relay
==============

Welcome to Dragon Relay, a system to control a Linux system using
Dragon NaturallySpeaking.


Prerequisites
=============

You will need a Linux host (I use Xubuntu) with

* GTK, xdotool + libxdo3, wmctrl, ØMQ
* Python 2.7 with python-gtk2, python-wnck, python-xlib, python-libxdo,
  tornado, pyzmq
* VirtualBox

and a Windows guest VM (I use Windows XP) with

* Host/guest networking set up
* Dragon Naturallyspeaking
* CPython 2.7, including pyzmq and Python for Windows Extensions
* IronPython 2.7

Python for Windows Extensions: http://sourceforge.net/projects/pywin32/
VirtIO virtual network drivers for Windows: http://www.linux-kvm.org/page/WindowsGuestDrivers/Download_Drivers

I'm currently using Dragon NaturallySpeaking 11.5 Premium; older Premium
editions should also work. Dragon 12 introduced some API changes that
broke the Python integration. Rumor has it that someone was working on
fixing it; try it at your own risk.

I do not know if the cheaper basic editions of NaturallySpeaking have
the necessary API support to make this system work; again, YMMV.


Hardware
--------

Most modern computers have enough horsepower to run Dragon reasonably,
even within a VM. Obviously the more RAM and CPU you can throw at it,
the better.

*The single most important hardware consideration is your audio input!*

Do not expect good recognition results with laptop audio hardware or a
cheap headset. For testing, experimenting, and play, cheap equipment is
fine, but if you plan to do any serious work you will need to invest in
a good audio input pipeline. My current setup is

* Audix OM7 handheld studio microphone
* InSync Buddy USB 7G ADC


Installation
============

.. caution::
    This is a complicated system with many moving parts. It can be
    tricky to get everything hooked together correctly. Don't expect to
    ``pip install dragon`` and have everything just work!

1. Get your VM set up

    a. Create a host-only adapter for dedicated host/guest communication
    b. Update Windows' hosts file, adding a ``vmhost`` alias to the
       VM host
    c. Set up a shared folder to hold your speech command files and other
       source. For convenience, you can map the share to a drive letter in
       Windows.

2. Install Dragon and complete its profile and training steps
3. Install NatLink
4. Install Dragonfly

Try running the relay::

    win_relay.bat
